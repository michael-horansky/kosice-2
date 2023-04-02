using CsvHelper.Configuration;
using Kosice.Model;

namespace Kosice.DataLoading.Mappers
{
    public sealed class RoadMapper : ClassMap<Road>
    {
        public RoadMapper()
        {
            Map(m => m.Begin);
            Map(m => m.End);
        }
    }
}