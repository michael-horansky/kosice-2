using CsvHelper.Configuration;
using Kosice.Model;

namespace Kosice.DataLoading.Mappers
{
    public sealed class IntersectionMapper : ClassMap<Intersection>
    {

        public IntersectionMapper()
        {
            Map(m => m.Id);
            Map(m => m.X);
            Map(m => m.Y);
        }
    }
}
