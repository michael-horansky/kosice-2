using Kosice.Model;

namespace Kosice.DataLoading.DataContext
{
    public class DataContext : IDataContext
    {
        public IReadOnlyList<Road> Roads { get; }

        public IReadOnlyList<Intersection> Intersections { get; }

        public IReadOnlyList<Building> Buildings { get; }


        public DataContext(IReadOnlyList<Intersection> intersections, IReadOnlyList<Road> roads, IReadOnlyList<Building> buildings)
        {
            Intersections = intersections;
            Roads = roads;
            Buildings = buildings;
        }
    }
}
