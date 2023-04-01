using System.Globalization;

namespace Kosice.Model
{
    /// <summary>
    /// Represents shark species
    /// </summary>
    public class Intersection: ObjectOnCoordinates
    {
        /// <summary>
        /// Unique identifier
        /// </summary>
        public int Id { get; set; }

        public Intersection()
        {

        }

        public Intersection(int id, float x, float y)
        {
            Id = id;
            X = X;
            Y = Y;
        }

        public override string ToString()
        {
            return $"Intersection at ({X}, {Y})";
        }

        protected bool Equals(Intersection other)
        {
            return Id == other.Id;
        }

        public override bool Equals(object? obj)
        {
            if (ReferenceEquals(null, obj)) return false;
            if (ReferenceEquals(this, obj)) return true;
            if (obj.GetType() != this.GetType()) return false;
            return Equals((Intersection)obj);
        }

        public override int GetHashCode()
        {
            return Id;
        }
    }
}
