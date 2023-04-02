using Kosice.DataLoading.DataContext;
using Kosice.DataLoading.Factory;
using Kosice.Model;
using Kosice.Model.Enums;

namespace Kosice
{
    public class BuildingManager
    {
        private IDataContext? _dataContext;
        public IDataContext DataContext => _dataContext ??= new DataContextFactory().CreateDataContext();

        /// <summary>
        /// Building manager
        /// </summary>

        public List<Building> GetBuildings()
        {
            return DataContext.Buildings.ToList();
        }


    }
}

