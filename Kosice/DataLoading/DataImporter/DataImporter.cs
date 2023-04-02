using System.Collections.ObjectModel;
using System.Globalization;
using CsvHelper;
using CsvHelper.Configuration;
using Kosice.Model;

namespace Kosice.DataLoading.DataImporter
{
    public class DataImporter : IDataImporter
    {
        #region csv_file_paths

        private static readonly string DataPath = Path.GetFullPath(@"../../../../importData/");

        private static readonly string RoadsCsvFilePath = DataPath + "roads.csv";

        private static readonly string IntersectionsCsvFilePath = DataPath + "intersections.csv";

        private static readonly string BuildingsCsvFilePath = DataPath + "POI_cleaned.csv";


        #endregion

        private readonly IList<Road> roads;

        private readonly IList<Intersection> intersections;

        private readonly IList<Building> buildings;


        public DataImporter()
        {
            roads = ImportFromCsv<Road>(RoadsCsvFilePath);
            intersections = ImportFromCsv<Intersection>(IntersectionsCsvFilePath);
            buildings = ImportFromCsv<Building>(BuildingsCsvFilePath);
        }

        public IReadOnlyList<Road> ListAllRoads()
        {
            return new ReadOnlyCollection<Road>(roads);
        }

        public IReadOnlyList<Intersection> ListAllIntersections()
        {
            return new ReadOnlyCollection<Intersection>(intersections);
        }

        public IReadOnlyList<Building> ListAllBuildings()
        {
            return new ReadOnlyCollection<Building>(buildings);
        }

        private IList<T> ImportFromCsv<T>(string filepath) where T : new()
        {
            using var reader = File.OpenText(filepath);
            var config = new CsvConfiguration(CultureInfo.InvariantCulture)
            {
                HasHeaderRecord = true,
                Delimiter = ";",
                HeaderValidated = null
            };

            using var csv = new CsvReader(reader, config);
            return csv.GetRecords<T>().ToList();
        }
    }
}
