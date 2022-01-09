#include "contiki.h"
#include "contiki-lib.h"
#include "contiki-net.h"
#include "net/ip/uip.h"
#include "net/ipv6/uip-ds6.h"
#include "net/rpl/rpl.h"

#include "net/netstack.h"
#include "dev/button-sensor.h"
#include "dev/slip.h"

//Include headers for light & accel. sensors
#include "dev/light-sensor.h"
#include "dev/acc-mag-sensor.h"
#include "dev/gyr-sensor.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "net/ip/uip-debug.h"
#include "httpd-simple.h"

static const char *TOP = "<html><head><title>ContikiRPL</title></head><body>\n";
static const char *SCRIPT = "<script src=\"script.js\"></script>\n";
static const char *BOTTOM = "</body></html>\n";
static char buf[512];
static int blen;
#define ADD(...) do {                                                   \
    blen += snprintf(&buf[blen], sizeof(buf) - blen, __VA_ARGS__);      \
  } while(0)

/* Configure Light sensor */
static void config_light()
{
  light_sensor.configure(LIGHT_SENSOR_SOURCE, ISL29020_LIGHT__AMBIENT);
  light_sensor.configure(LIGHT_SENSOR_RESOLUTION, ISL29020_RESOLUTION__16bit);
  light_sensor.configure(LIGHT_SENSOR_RANGE, ISL29020_RANGE__1000lux);
  SENSORS_ACTIVATE(light_sensor);
}

/* Configure Accelerometer */
static unsigned acc_freq = 0;
static float speed_acc = 0; //calculated speed from acceleration
static int time_interval = 0; //time interval between 2 measurements
static void config_acc()
{
  acc_sensor.configure(ACC_MAG_SENSOR_DATARATE, LSM303DLHC_ACC_RATE_1344HZ_N_5376HZ_LP);
  acc_freq = 1344;
  acc_sensor.configure(ACC_MAG_SENSOR_SCALE, LSM303DLHC_ACC_SCALE_2G);
  acc_sensor.configure(ACC_MAG_SENSOR_MODE, LSM303DLHC_ACC_UPDATE_ON_READ);
  SENSORS_ACTIVATE(acc_sensor);
}


static int xyz[3] = {0, 0, 0};
static void process_acc()
{
  static unsigned count = 0;
  if ((++count % acc_freq) == 0) {
    xyz[0] = acc_sensor.value(ACC_MAG_SENSOR_X);
    xyz[1] = acc_sensor.value(ACC_MAG_SENSOR_Y);
    xyz[2] = acc_sensor.value(ACC_MAG_SENSOR_Z);
  }
}

/* Gyroscope */
static unsigned gyr_freq = 0;
static void config_gyr()
{
  gyr_sensor.configure(GYR_SENSOR_DATARATE, L3G4200D_800HZ);
  gyr_freq = 800;
  gyr_sensor.configure(GYR_SENSOR_SCALE, L3G4200D_250DPS);
  SENSORS_ACTIVATE(gyr_sensor);
}

static int xyz_gyr[3];
static void process_gyr()
{
  static unsigned count = 0;
  if ((++count % gyr_freq) == 0) {
    xyz_gyr[0] = gyr_sensor.value(GYR_SENSOR_X);
    xyz_gyr[1] = gyr_sensor.value(GYR_SENSOR_Y);
    xyz_gyr[2] = gyr_sensor.value(GYR_SENSOR_Z);
  }
}


/*---------------------------------------------------------------------------*/
PROCESS(webserver_process, "Luminosity and acceleration");
PROCESS_THREAD(webserver_process, ev, data)
{
  PROCESS_BEGIN();

  httpd_init();

  while(1) {
    PROCESS_WAIT_EVENT_UNTIL(ev == tcpip_event);
    httpd_appcall(data);
  }
  
  PROCESS_END();
}

/*---------------------------------------------------------------------------*/
PROCESS(sensor_collection, "Accelerometer & gyroscope data collection");
PROCESS_THREAD(sensor_collection, ev, data)
{
  PROCESS_BEGIN();
  static struct timer timer;

  //timer_set(&timer, CLOCK_SECOND);

  config_acc();
  config_gyr();

  while(1) {
    PROCESS_WAIT_EVENT();
    if (ev == PROCESS_EVENT_TIMER) {

     //accelerometer : xyz[0] in mg => convert to g
      float accel = (float)xyz[1];
      speed_acc = (speed_acc + accel/1000);
      timer_restart(&timer);

    } else if (ev == sensors_event && data == &acc_sensor) {
      //time_interval = 30*CLOCK_SECOND - timer_remaining(&timer);
      process_acc();
      //timer_restart(&timer);
    } else if (ev == sensors_event && data == &gyr_sensor) {
      process_gyr();
    }
  }

  PROCESS_END();
}

AUTOSTART_PROCESSES(&webserver_process, &sensor_collection);
/*---------------------------------------------------------------------------*/
static void
ipaddr_add(const uip_ipaddr_t *addr)
{
  uint16_t a;
  int i, f;
  for(i = 0, f = 0; i < sizeof(uip_ipaddr_t); i += 2) {
    a = (addr->u8[i] << 8) + addr->u8[i + 1];
    if(a == 0 && f >= 0) {
      if(f++ == 0) ADD("::");
    } else {
      if(f > 0) {
        f = -1;
      } else if(i > 0) {
        ADD(":");
      }
      ADD("%x", a);
    }
  }
}

/*---------------------------------------------------------------------------*/
static
PT_THREAD(generate_script(struct httpd_state *s))
{
  PSOCK_BEGIN(&s->sout);
  SEND_STRING(&s->sout, "\
  onload=function() {\
	p=location.host.replace(/::.*/,'::').substr(1);\
	a=document.getElementsByTagName('a');\
	for(i=0;i<a.length;i++) {\
		txt=a[i].innerHTML.replace(/^FE80::/,p);\
		a[i].href='http://['+txt+']';\
	}\
  }");
  PSOCK_END(&s->sout);
}
/*---------------------------------------------------------------------------*/
static
PT_THREAD(generate_routes(struct httpd_state *s))
{
  static uip_ds6_route_t *r;
  static uip_ds6_nbr_t *nbr;

  static uip_ipaddr_t *preferred_parent_ip;
  { /* assume we have only one instance */
    rpl_dag_t *dag = rpl_get_any_dag();
    preferred_parent_ip = rpl_get_parent_ipaddr(dag->preferred_parent);
  }

  PSOCK_BEGIN(&s->sout);

  blen = 0;

  // Light Sensor
  config_light();

  int light_val = light_sensor.value(0);
  float light = ((float)light_val) / LIGHT_SENSOR_VALUE_SCALE;
  
  // ADD adds the printline into the buffer buf
  ADD("{\"luminosite\":%f}\n",light);

  //ADD("{\"accel_x\": %d, \"accel_y\":%d, \"accel_z\":%d}\n", xyz[0], xyz[1], xyz[2]);
  ADD("{\"vitesse\":%f}\n",speed_acc);
  
  //gyroscope : angular speed for x axis
  ADD("%d\n", -xyz_gyr[0]);

  ADD("time interval:%d",time_interval);

  SEND_STRING(&s->sout, buf);
  
  blen = 0;
  PSOCK_END(&s->sout);
}

/*---------------------------------------------------------------------------*/
httpd_simple_script_t
httpd_simple_get_script(const char *name)
{
  if (!strcmp("script.js", name))
    return generate_script;
  else 
    return generate_routes;
}
