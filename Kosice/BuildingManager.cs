using Kosice.DataLoading.DataContext;
using Kosice.DataLoading.Factory;
using Kosice.Model;
using Kosice.Model.Enums;
using CsvHelper.Configuration;
using System.Globalization;
using CsvHelper;

namespace Kosice
{
    public class BuildingManager
    {
        private IDataContext? _dataContext;
        private int highestId;
        public List<Building> Buildings { get; set; }
        public IDataContext DataContext => _dataContext ??= new DataContextFactory().CreateDataContext();
        private IDataContext newData;
        private string importDataPath;
        private CsvConfiguration config = new CsvConfiguration(CultureInfo.InvariantCulture)
        {
            HasHeaderRecord = true,
            Delimiter = ";"
        };
        /// <summary>
        /// Building manager
        /// </summary>
        /// 
        public BuildingManager()
        {
            highestId = DataContext.Buildings
                .OrderByDescending(x=> x.Id)
                .First().Id;
            Buildings = GetBuildings();
            importDataPath = Path.GetFullPath(@"../../../../importData/");


        }

        public List<Building> GetBuildings()
        {
            newData = new DataContextFactory().CreateDataContext();
            return DataContext.Buildings.ToList();
        }

        public void AddBuilding(string name, BuildingType buildingType, float x, float y)
        {
            var newBuilding = new Building( highestId ++, name, buildingType, y, x);
            Buildings.Add(newBuilding);

            using (var writer = new StreamWriter(importDataPath + "POI-cleaned.csv"))
            using (var csv = new CsvWriter(writer, config))
            {
                csv.WriteRecords(Buildings);
            }
        }


    }
}

