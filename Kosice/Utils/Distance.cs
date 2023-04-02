using Kosice.Model;
using QuickGraph;
using QuickGraph.Algorithms.ShortestPath;

namespace Kosice.Utils
{

    public class Distance
    {
        private AdjacencyGraph<string, TaggedEdge<string, double>> G { get; }
        private Dictionary<int, Intersection> intersections { get; set; }

        public Distance(Dictionary<int, Intersection> intersections)
        {
            this.G = new AdjacencyGraph<string, TaggedEdge<string, double>>();
            this.intersections = intersections;
        }

        public void addIntersection(Intersection intersection)
        {
            G.AddVertex(intersection.Id.ToString());
        }

        public void addRoad(Road road)
        {
            G.AddEdge(new TaggedEdge<string, double>(
                this.intersections[road.FromId].Id.ToString(),
                this.intersections[road.ToId].Id.ToString(),
                road.PhysicalLength(this.intersections)
                )
            );
        }

        public float GetShortestPathWeight(Intersection int1, Intersection int2)
        {
            var algorithm = new DijkstraShortestPathAlgorithm<string, TaggedEdge<string, double>>(this.G, e => e.Tag);
            algorithm.Compute(int1.Id.ToString());

            double shortestPathWeight;
            if (algorithm.TryGetDistance(int2.Id.ToString(), out shortestPathWeight))
            {
                return (float) shortestPathWeight;
            }
            else
            {
                // There's no path from int1 to int2
                return float.PositiveInfinity;
            }
        }
    }

}

