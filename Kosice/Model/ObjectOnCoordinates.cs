using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Kosice.Model
{
    public class ObjectOnCoordinates
    {
        /// <summary>
        /// longitude
        /// </summary>
        public float X { get; set; }

        /// <summary>
        /// lattitude
        /// </summary>
        public float Y { get; set; }

        public Tuple<float, float> GetPair()
        {
            return new Tuple<float, float>(this.X, this.Y);
        }

        public float ConvertToRadians(float angle)
        {
            return (float) (Math.PI / 180) * angle;
        }

        public Tuple<float, float, float> AbsolutePosition()
        {
            var earth_radius = (float) 6.371e06;
            var x = (float) (Math.Cos(ConvertToRadians(this.X)) * Math.Cos(ConvertToRadians(this.Y)) * earth_radius);
            var y = (float) (Math.Sin(ConvertToRadians(this.X)) * Math.Cos(ConvertToRadians(this.Y)) * earth_radius);
            var z = (float) (Math.Sin(ConvertToRadians(this.Y)) * earth_radius);
            return new Tuple<float, float, float>(x, y, z);
        }

        public Tuple<float, float, bool> DistanceFromGreatArc(ObjectOnCoordinates loc1, ObjectOnCoordinates loc2)
        {
            Tuple<float, float, float> ThisPosition = this.AbsolutePosition();
            float X = ThisPosition.Item1;
            float Y = ThisPosition.Item2;
            float Z = ThisPosition.Item3;

            Tuple<float, float, float> Loc1Position = loc1.AbsolutePosition();
            float X1 = Loc1Position.Item1;
            float Y1 = Loc1Position.Item2;
            float Z1 = Loc1Position.Item3;

            Tuple<float, float, float> Loc2Position = loc2.AbsolutePosition();
            float X2 = Loc2Position.Item1;
            float Y2 = Loc2Position.Item2;
            float Z2 = Loc2Position.Item3;

            float Q_cross_R_x = Y1 * Z2 - Y2 * Z1;
            float Q_cross_R_y = Z1 * X2 - Z2 * X1;
            float Q_cross_R_z = X1 * Y2 - X2 * Y1;

            float size_Q_cross_R = (float) Math.Sqrt(Q_cross_R_x * Q_cross_R_x + Q_cross_R_y * Q_cross_R_y + Q_cross_R_z * Q_cross_R_z);
            Q_cross_R_x = Q_cross_R_x / size_Q_cross_R;
            Q_cross_R_y = Q_cross_R_y / size_Q_cross_R;
            Q_cross_R_z = Q_cross_R_z / size_Q_cross_R;

            float P_dot_Q_cross_R = (float) Math.Abs(X * Q_cross_R_x + Y * Q_cross_R_y + Z * Q_cross_R_z);
            float pos_on_road_x = X - P_dot_Q_cross_R * Q_cross_R_x;
            float pos_on_road_y = Y - P_dot_Q_cross_R * Q_cross_R_y;
            float pos_on_road_z = Z - P_dot_Q_cross_R * Q_cross_R_z;

            float d1_x = pos_on_road_x - X1;
            float d1_y = pos_on_road_y - Y1;
            float d1_z = pos_on_road_z - Z1;
            float d2_x = X2 - pos_on_road_x;
            float d2_y = Y2 - pos_on_road_y;
            float d2_z = Z2 - pos_on_road_z;

            bool shortest_distance_lies_on_arc = d1_x * d2_x + d1_y * d2_y + d1_z * d2_z > 0;

            float distance_along_road = (float) Math.Sqrt((X1 - pos_on_road_x) * (X1 - pos_on_road_x) + (Y1 - pos_on_road_y) * (Y1 - pos_on_road_y) + (Z1 - pos_on_road_z) * (Z1 - pos_on_road_z));
            return new Tuple<float, float, bool>(P_dot_Q_cross_R, distance_along_road, shortest_distance_lies_on_arc);
        }


        public float DistanceToOtherLocation(ObjectOnCoordinates other)
        {
            float lon1rad = ConvertToRadians(this.X);
            float lat1rad = ConvertToRadians(this.Y);

            float lon2rad = ConvertToRadians(other.X);
            float lat2rad = ConvertToRadians(other.Y);

            return (float) Math.Acos(Math.Sin(lat1rad) * Math.Sin(lat2rad) + Math.Cos(lat1rad) * Math.Cos(lat2rad) * Math.Cos(lon2rad - lon1rad));
        }

        public Tuple<float, float> DistanceToRoad(Road road, Dictionary<int, Intersection> intersections)
        {

            Tuple<float, float, bool> DistanceFromGreatArc = this.DistanceFromGreatArc(intersections[road.Begin], intersections[road.End]);
            float DistanceFromRoadArc = DistanceFromGreatArc.Item1;
            float DistanceAlongRoad = DistanceFromGreatArc.Item2;
            bool UseArc = DistanceFromGreatArc.Item3;

            float DistanceFromFirstIntersection = this.DistanceToOtherLocation(intersections[road.Begin]);
            float DistanceFromSecondIntersection = this.DistanceToOtherLocation(intersections[road.End]);

            if (UseArc)
            {
                return new Tuple<float, float>(DistanceFromRoadArc, DistanceAlongRoad);
            }

            if (DistanceFromFirstIntersection < DistanceFromSecondIntersection)
            {
                return new Tuple<float, float>(DistanceFromFirstIntersection, 0);
            }
            else //if (DistanceFromSecondIntersection < DistanceFromFirstIntersection)
            {
                return new Tuple<float, float>(DistanceFromSecondIntersection, road.PhysicalLength(intersections));
            }
        }
    }
}
