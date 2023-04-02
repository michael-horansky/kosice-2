using System.Collections.Generic;
using Kosice.DataLoading.DataContext;
using Kosice.DataLoading.Factory;
using Kosice.Model;
using Kosice.Utils;
using Kosice.Model.Enums;

namespace Kosice
{
    public class Queries
    {
        private IDataContext? _dataContext;
        public IDataContext DataContext => _dataContext ??= new DataContextFactory().CreateDataContext();

        /// <summary>
        /// Ukážkové query na pripomenutie základnej LINQ syntaxe a operátorov. Výsledky nie je nutné vracať
        /// pomocou jedného príkazu, pri zložitejších queries je vhodné si vytvoriť pomocné premenné cez `var`.
        /// Toto query nie je súčasťou hodnotenia.
        /// </summary>
        /// <returns>The query result</returns>
        public List<Road> getRoads()
        {
            return DataContext.Roads.ToList();
        }

        public List<Intersection> GetIntersections()
        {
            return DataContext.Intersections.ToList();
        }

        public List<Building> GetBuildings()
        {
            return DataContext.Buildings.ToList();
        }
    }

    public class Computing
    {

        Distance distance { get; set; }
        Dictionary<string, float> DefaultTransportationSpeeds { get; } = new Dictionary<string, float> {
            {"walk",1}, {"bike",6}, {"car",10}
        };

        public Computing(Dictionary<int, Intersection> intersections)
        {
            this.distance = new Distance(intersections);
        }

        public float ShortestPathBetweenTwoIntersections( Intersection StartIntersection, List<Intersection> EndIntersections, string ModeOfTtransportation)
        {
            float length = Math.Min(
                this.distance.GetShortestPathWeight(StartIntersection, EndIntersections[0]),
                this.distance.GetShortestPathWeight(StartIntersection, EndIntersections[1])
                );

            return length / DefaultTransportationSpeeds[ModeOfTtransportation];
        }

    }
}