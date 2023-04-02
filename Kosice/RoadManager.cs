using Kosice.DataLoading.DataContext;
using Kosice.DataLoading.Factory;
using Kosice.Model;
using Kosice.Model.Enums;
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
        private List<Intersection> intersections = new List<Intersection>();
        private CsvConfiguration config = new CsvConfiguration(CultureInfo.InvariantCulture)
        {
            HasHeaderRecord = true,
            Delimiter = ";"
        };
            
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

        public List<Intersection> GetIntersections()
        {
            var newData = new DataContextFactory().CreateDataContext();

            return newData.Intersections.ToList();
        }

        public void AddIntersection(float x, float y)
        {
            var newIntersection = new Intersection(highestId++, x, y);
            intersections.Add(newIntersection);

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
            if (!intersections.Any(x => x.Id == id))
            { return false; }
            intersections = intersections.Where(x => x.Id != id).ToList();
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

