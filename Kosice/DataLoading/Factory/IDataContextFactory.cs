using Kosice.DataLoading.DataContext;

namespace Kosice.DataLoading.Factory
{
    public interface IDataContextFactory
    {
        IDataContext CreateDataContext();
    }
}
