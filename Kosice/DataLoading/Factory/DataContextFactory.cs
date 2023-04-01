using Kosice.DataLoading.DataContext;

namespace Kosice.DataLoading.Factory
{
    public class DataContextFactory : IDataContextFactory
    {
        public IDataContext CreateDataContext()
        {
            var importer = new DataImporter.DataImporter();
            return new DataContext.DataContext(importer.ListAllIntersections(),
                importer.ListAllRoads(),
                importer.ListAllBuildings());
        }
    }
}
