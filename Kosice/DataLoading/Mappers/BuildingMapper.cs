using CsvHelper.Configuration;
using Kosice.Model;

namespace Kosice.DataLoading.Mappers
{
    public sealed class BuildingMapper : ClassMap<Building>
    {

        public BuildingMapper()
        {
            Map(m => m.Id);
            Map(m => m.X);
            Map(m => m.Y);
            Map(m => m.BuildType);
            
        }
    }
}
