using System.Collections.Generic;
using Kosice.DataLoading.DataContext;
using Kosice.DataLoading.Factory;
using Kosice.Model;
using Kosice.Utils;
using Kosice.Model.Enums;
using System;
using System.Collections;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Kosice;

class program
{
    static void Main()
    {
        RoadManager roadManager = new();
        //foreach (var road in roadManager.GetRoads())
        //{
        //    Console.WriteLine(road);
        //}
        Console.WriteLine(roadManager.GetRoads().Count);
        roadManager.AddRoad(4846566, 46);
        Console.WriteLine(roadManager.GetRoads().Count);
        roadManager.RemoveIntersection(4846566);
        Console.WriteLine(roadManager.GetRoads().Count);
        Console.ReadLine();
    }

    public class Computing
    {

        public const int DirectPathThreshold = 20;

        Distance distance { get; set; }
        Dictionary<string, float> DefaultTransportationSpeeds { get; } = new Dictionary<string, float> {
            {"walk",1}, {"bike",6}, {"car",10}
        };
        List<Road> roads { get; set; }
        Dictionary<int, Intersection> intersections { get; }

        public Computing(Dictionary<int, Intersection> intersections, List<Road> roads)
        {
            this.distance = new Distance(intersections);
            this.intersections = intersections;
            this.roads = roads;
        }

        public float ShortestPathBetweenTwoIntersections(Intersection StartIntersection, List<Intersection> EndIntersections, string ModeOfTtransportation)
        {
            float length = Math.Min(
                this.distance.GetShortestPathWeight(StartIntersection, EndIntersections[0]),
                this.distance.GetShortestPathWeight(StartIntersection, EndIntersections[1])
                );

            return length / DefaultTransportationSpeeds[ModeOfTtransportation];
        }

        public List<Road> NMaxElements(List<Road> list1, int N, Func<Road, float> EvalFunction)
        {
            List<Road> InitList = new List<Road>(list1);
            List<Road> FinalList = new List<Road>();

            for (int i = 0; i < N; i++)
            {
                float Max1 = EvalFunction(InitList[0]);
                int Index1 = 0;

                for (int j = 1; j < InitList.Count(); j++)
                {
                    if (EvalFunction(InitList[j]) > Max1)
                    {
                        Max1 = EvalFunction(InitList[j]);
                        Index1 = j;
                    }
                }

                FinalList.Append(InitList[Index1]);
                InitList.RemoveAt(Index1);
            }

            return FinalList;
        }

        public Tuple<Road, float, float> FindDistanceToNearestRoad(ObjectOnCoordinates StartLocation)
        {
            Road NearestRoad = this.NMaxElements(this.roads, 1, (x) => { return -1 * StartLocation.DistanceToRoad(x, intersections).Item1; })[0];
            Tuple<float, float> DistanceFromRoadResult = StartLocation.DistanceToRoad(NearestRoad, intersections);

            return new Tuple<Road, float, float>(NearestRoad, DistanceFromRoadResult.Item1, DistanceFromRoadResult.Item2);
        }

        public float FindPathBetweenTwoLocations(
            ObjectOnCoordinates StartLocation,
            ObjectOnCoordinates EndLocation,
            string ModeOfTransportation
        )
        {
            if (StartLocation.DistanceToOtherLocation(EndLocation) < DirectPathThreshold)
            {
                return StartLocation.DistanceToOtherLocation(EndLocation);
            }

            Tuple<Road, float, float> StartDistancesToNearestRoad = this.FindDistanceToNearestRoad(StartLocation);
            Road StartNearestRoad = StartDistancesToNearestRoad.Item1;
            float StartDistanceToRoad = StartDistancesToNearestRoad.Item2;
            float StartRoadOffset = StartDistancesToNearestRoad.Item3;

            Tuple<Road, float, float> EndDistancesToNearestRoad = this.FindDistanceToNearestRoad(EndLocation);
            Road EndNearestRoad = EndDistancesToNearestRoad.Item1;
            float EndDistanceToRoad = EndDistancesToNearestRoad.Item2;
            float EndRoadOffset = EndDistancesToNearestRoad.Item3;

            List<Intersection> EndRoadIntersections = new List<Intersection>() { intersections[EndNearestRoad.Begin], intersections[EndNearestRoad.End] };
            float DistanceFromFirstStartIntersection = this.ShortestPathBetweenTwoIntersections(intersections[StartNearestRoad.Begin], EndRoadIntersections, ModeOfTransportation);
            float DistanceFromSecondStartIntersection = this.ShortestPathBetweenTwoIntersections(intersections[StartNearestRoad.End], EndRoadIntersections, ModeOfTransportation);

            float WalkingPart = (StartDistanceToRoad + EndDistanceToRoad) / DefaultTransportationSpeeds["walk"];

            float D1_1 =
                WalkingPart
                + (StartRoadOffset / DefaultTransportationSpeeds[ModeOfTransportation])
                + (EndRoadOffset / DefaultTransportationSpeeds[ModeOfTransportation])
                + DistanceFromFirstStartIntersection;
            float D1_2 =
                WalkingPart
                + (StartRoadOffset / DefaultTransportationSpeeds[ModeOfTransportation])
                + (
                    (EndNearestRoad.PhysicalLength(intersections) - EndRoadOffset)
                    / DefaultTransportationSpeeds[ModeOfTransportation]
                )
                + DistanceFromSecondStartIntersection;
            float D2_1 =
                WalkingPart
                + (
                    (StartNearestRoad.PhysicalLength(intersections) - StartRoadOffset)
                    / DefaultTransportationSpeeds[ModeOfTransportation]
                )
                + (EndRoadOffset / DefaultTransportationSpeeds[ModeOfTransportation])
                + DistanceFromFirstStartIntersection;
            float D2_2 =
                WalkingPart
                + (
                    (StartNearestRoad.PhysicalLength(intersections) - StartRoadOffset)
                    / DefaultTransportationSpeeds[ModeOfTransportation]
                )
                + (
                    (EndNearestRoad.PhysicalLength(intersections) - EndRoadOffset)
                    / DefaultTransportationSpeeds[ModeOfTransportation]
                )
                + DistanceFromSecondStartIntersection;

            float min = D1_1;
            if (D1_2 < min)
            {
                min = D1_2;
            }
            if (D2_1 < min)
            {
                min = D2_1;
            }
            if (D2_2 < min)
            {
                min = D2_2;
            }

            return min;
        }
    }
}