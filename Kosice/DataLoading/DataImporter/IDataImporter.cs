using System.Collections.ObjectModel;
using Kosice.Model;

namespace Kosice.DataLoading.DataImporter
{
    public interface IDataImporter
    {
        IReadOnlyList<Road> ListAllRoads();
        IReadOnlyList<Building> ListAllBuildings();
        IReadOnlyList<Intersection> ListAllIntersections();
    }
}