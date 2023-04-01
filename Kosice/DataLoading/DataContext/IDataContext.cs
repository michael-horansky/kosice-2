using Kosice.Model;

namespace Kosice.DataLoading.DataContext
{
    public interface IDataContext
    {
        IReadOnlyList<Road> Roads { get; }
        IReadOnlyList<Intersection> Intersections { get; }
        IReadOnlyList<Building> Buildings { get; }
    }
}