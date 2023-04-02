using Kosice.DataLoading.DataContext;
using Kosice.DataLoading.Factory;
using Kosice.Model;
using Kosice.Model.Enums;

namespace Kosice
{
    public class Queries
    {
        private IDataContext? _dataContext;
        public IDataContext DataContext => _dataContext ??= new DataContextFactory().CreateDataContext();

        /// <summary>
        /// Ukážkové query na pripomenutie základnej LINQ syntaxe a operátorov. Výsledky nie je nutné vracať
        /// pomocou jedného príkazu, pri zložitejších queries je vhodné si vytvoriť pomocné premenné cez `var`.
        /// Toto query nie je súčasťou hodnotenia.
        /// </summary>
        /// <returns>The query result</returns>
        public List<Road> getRoads()
        {
            return DataContext.Roads.ToList();
        }

        public List<Intersection> GetIntersections()
        {
            return DataContext.Intersections.ToList();
        }

        public List<Building> GetBuildings()
        {
            return DataContext.Buildings.ToList();
        }
    }

    public class Computing
    {

    }
}