using CsvHelper.Configuration;
using Kosice.Model;

namespace Kosice.DataLoading.Mappers
{
    public sealed class RoadMapper : ClassMap<Road>
    {
        public RoadMapper()
        {
            Map(m => m.FromId);
            Map(m => m.ToId);
        }
    }
}