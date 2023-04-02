using Kosice.DataLoading.DataContext;
using Kosice.DataLoading.Factory;
using Kosice.Model;
using Kosice.Utils;
using CsvHelper;
using System.Globalization;
using CsvHelper.Configuration;

namespace Kosice
{
    public class RoadManager
    {
        private IDataContext? _dataContext;
        public IDataContext DataContext => _dataContext ??= new DataContextFactory().CreateDataContext();
        public int highestId;
        private string importDataPath;
        private List<Road> roads = new List<Road>();
        private Dictionary<int, Intersection> intersections = new Dictionary<int, Intersection>();
        private CsvConfiguration config = new CsvConfiguration(CultureInfo.InvariantCulture)
        {
            HasHeaderRecord = true,
            Delimiter = ";"
        };

        public EventHandler<ObjectOnCoordinatesEventArgs> ObjectAdded;

        protected virtual void OnObjectAdded(ObjectOnCoordinates objectOnCoordinates)
        {
            if (ObjectAdded != null)
            {
                var args = new ObjectOnCoordinatesEventArgs(objectOnCoordinates);
                ObjectAdded(this, args);
            }
        }



        public RoadManager()
        {
            highestId = DataContext.Intersections
                .OrderByDescending(x=> x.Id).First().Id;
            importDataPath = Path.GetFullPath(@"../../../../importData/");
            roads = GetRoads();
            intersections = GetIntersections();

        }

        /// <summary>
        /// Manager for Intersections and roads
        /// </summary>

        public List<Road> GetRoads()
        {
            var newData = new DataContextFactory().CreateDataContext();
            return newData.Roads.ToList();
        }

        public Dictionary<int,Intersection> GetIntersections()
        {
            var newData = new DataContextFactory().CreateDataContext();

            return newData.Intersections.ToDictionary(x => x.Id, y => y);
        }

        public void AddIntersection(float x, float y)
        {
            var newIntersection = new Intersection(highestId++, x, y);
            intersections.Add(newIntersection.Id, newIntersection);

            using (var writer = new StreamWriter(importDataPath + "intersections.csv"))
            using (var csv = new CsvWriter(writer, config))
            {
                csv.WriteRecords(intersections);
            }
        }

        public void AddRoad(int begin, int end)
        {
            var newRoad = new Road(begin, end);
            roads.Add(newRoad);

            using (var writer = new StreamWriter(importDataPath + "roads.csv"))
            using (var csv = new CsvWriter(writer, config))
            {
                csv.WriteRecords(roads);
            }
        }
        public bool RemoveIntersection(int id)
        {
            if (!intersections.Any(x => x.Key == id))
            { return false; }
            intersections = intersections.Where(x => x.Key != id).ToDictionary(a=>a.Key, b => b.Value);

            roads = roads.Where(x => x.Begin == id || x.End == id).ToList();
            using (var writer = new StreamWriter(importDataPath + "intersections.csv"))
            using (var csv = new CsvWriter(writer, config))
            {
                csv.WriteRecords(intersections);
            }
            using (var writer = new StreamWriter(importDataPath + "roads.csv"))
            using (var csv = new CsvWriter(writer, config))
            {
                csv.WriteRecords(roads);
            }
            return true;
        }
        public bool RemoveRoad(int begin, int end)
        {
            if (!roads.Any(x => x.Begin == begin && x.End==end))
            { return false; }
            roads = roads.Where(x => (x.Begin != begin || x.End != end) && (x.Begin != end || x.End != begin)).ToList();
            using (var writer = new StreamWriter(importDataPath + "roads.csv"))
            using (var csv = new CsvWriter(writer, config))
            {
                csv.WriteRecords(roads);
            }
            return true;
        }
    }
}

