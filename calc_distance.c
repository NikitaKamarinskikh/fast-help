#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>

float radians(float x) {
    return x / (180 / M_PI);
}

int calc_distance(float lat1, float lon1, float lat2, float lon2) {
    lat1 = radians(lat1);
    lon1 = radians(lon1);
    lat2 = radians(lat2);
    lon2 = radians(lon2);
    float delta_lon = lon2 - lon1;
    float delta_lat = lat2 - lat1;
    float a = pow(sin(delta_lat / 2.0), 2) + cos(lat1) * cos(lat2) * pow(sin(delta_lon / 2.0), 2);
    float c = 2 * atan2(sqrt(a), sqrt(1 - a));
    float distance = 6378.1 * c * 1000;
    return round(distance);
}

int main(int argc, char **argv) {
    FILE *file = fopen(*&argv[1], "r");
    FILE *result_file = fopen(*&argv[2], "w+");
    char str[BUFSIZ] = "";
    while (fgets(str, BUFSIZ, file)) {
        short x = 0;
        float lat1 = 0.0, lon1 = 0.0, lat2 = 0.0, lon2 = 0.0;
        char *pch = strtok(str, " ");
        while (NULL != pch) {
            if (x == 0) {
                lat1 = atof(pch);
            } else if (x == 1) {
                lon1 = atof(pch);
            } else if (x == 2) {
                lat2 = atof(pch);
            } else if (x == 3) {
                lon2 = atof(pch);
            }
            pch = strtok(NULL, " ");
            x++;
        }
        fprintf(result_file, "%d\n", calc_distance(lat1, lon1, lat2, lon2));
    }
    fclose(file);
    fclose(result_file);
}

