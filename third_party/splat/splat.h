#ifndef SPLAT_H
#define SPLAT_H

#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <bzlib.h>
#include <unistd.h>

#define HD_MODE 0
#define MAXPAGES 25

#define GAMMA 2.5
#define BZBUFFER 65536

#if HD_MODE==0
    #if MAXPAGES==4
    #define ARRAYSIZE 4950
    #endif

    #if MAXPAGES==9
    #define ARRAYSIZE 10870
    #endif

    #if MAXPAGES==16
    #define ARRAYSIZE 19240
    #endif

    #if MAXPAGES==25
    #define ARRAYSIZE 30025
    #endif

    #if MAXPAGES==36
    #define ARRAYSIZE 43217
    #endif

    #if MAXPAGES==49
    #define ARRAYSIZE 58813
    #endif

    #if MAXPAGES==64
    #define ARRAYSIZE 76810
    #endif

    #define IPPD 1200
#endif

#if HD_MODE==1
    #if MAXPAGES==1
    #define ARRAYSIZE 5092 
    #endif

    #if MAXPAGES==4
    #define ARRAYSIZE 14844 
    #endif

    #if MAXPAGES==9
    #define ARRAYSIZE 32600
    #endif

    #if MAXPAGES==16
    #define ARRAYSIZE 57713
    #endif

    #if MAXPAGES==25
    #define ARRAYSIZE 90072
    #endif

    #if MAXPAGES==36
    #define ARRAYSIZE 129650
    #endif

    #if MAXPAGES==49 
    #define ARRAYSIZE 176437
    #endif

    #if MAXPAGES==64
    #define ARRAYSIZE 230430
    #endif

    #define IPPD 3600
#endif

#ifndef PI
#define PI 3.141592653589793
#endif

#ifndef TWOPI
#define TWOPI 6.283185307179586
#endif

#ifndef HALFPI
#define HALFPI 1.570796326794896
#endif

#define DEG2RAD 1.74532925199e-02
#define EARTHRADIUS 20902230.97
#define METERS_PER_MILE 1609.344
#define METERS_PER_FOOT 0.3048
#define KM_PER_MILE 1.609344
#define FOUR_THIRDS 1.3333333333333

struct site {
    double lat;
    double lon;
    float alt;
    char name[50];
    char filename[255];
};

struct path {
    double lat[ARRAYSIZE];
    double lon[ARRAYSIZE];
    double elevation[ARRAYSIZE];
    double distance[ARRAYSIZE];
    int length;
};

struct dem {
    int min_north;
    int max_north;
    int min_west;
    int max_west;
    int max_el;
    int min_el;
    short data[IPPD][IPPD];
    unsigned char mask[IPPD][IPPD];
    unsigned char signal[IPPD][IPPD];
};

struct LR {
    double eps_dielect; 
    double sgm_conductivity; 
    double eno_ns_surfref;
    double frq_mhz; 
    double conf; 
    double rel;
    double erp;
    int radio_climate;  
    int pol;
    float antenna_pattern[361][1001];
};

struct region {
    unsigned char color[32][3];
    int level[32];
    int levels;
};

extern char string[255], sdf_path[255], opened, gpsav, splat_name[10], splat_version[6], dashes[80], olditm;
extern double earthradius, max_range, forced_erp, dpp, ppd, fzone_clearance, forced_freq, clutter;
extern int min_north, max_north, min_west, max_west, ippd, mpi, max_elevation, min_elevation, bzerror, contour_threshold;
extern unsigned char got_elevation_pattern, got_azimuth_pattern, metric, dbm, smooth_contours;
extern struct site site;
extern struct path path;
extern struct dem dem[MAXPAGES];
extern struct LR LR;
extern struct region region;
extern double elev[ARRAYSIZE+10];

void point_to_point(double elev[], double tht_m, double rht_m, double eps_dielect, double sgm_conductivity, double eno_ns_surfref, double frq_mhz, int radio_climate, int pol, double conf, double rel, double &dbloss, char *strmode, int &errnum);
void point_to_point_ITM(double elev[], double tht_m, double rht_m, double eps_dielect, double sgm_conductivity, double eno_ns_surfref, double frq_mhz, int radio_climate, int pol, double conf, double rel, double &dbloss, char *strmode, int &errnum);
double ITWOMVersion();
int interpolate(int y0, int y1, int x0, int x1, int n);
double arccos(double x, double y);
int ReduceAngle(double angle);
double LonDiff(double lon1, double lon2);
char *dec2dms(double decimal);
int PutMask(double lat, double lon, int value);
int OrMask(double lat, double lon, int value);
int GetMask(double lat, double lon);
int PutSignal(double lat, double lon, unsigned char signal);
unsigned char GetSignal(double lat, double lon);
double GetElevation(struct site location);
int AddElevation(double lat, double lon, double height);
double Distance(struct site site1, struct site site2);
double Azimuth(struct site source, struct site destination);
double ElevationAngle(struct site source, struct site destination);
void ReadPath(struct site source, struct site destination);
double ElevationAngle2(struct site source, struct site destination, double er);
double AverageTerrain(struct site source, double azimuthx, double start_distance, double end_distance);
double haat(struct site antenna);
void PlaceMarker(struct site location);
double ReadBearing(char *input);
struct site LoadQTH(char *filename);
void LoadPAT(char *filename);
int LoadSDF_SDF(char *name);

#endif // SPLAT_H