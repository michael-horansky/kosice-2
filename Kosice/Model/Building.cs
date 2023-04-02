using System.Globalization;
using Kosice.Model.Enums;

namespace Kosice.Model
{
    /// <summary>
    /// Represents country, where the shark attack occured.
    /// </summary>
    public class Building: ObjectOnCoordinates
    {
        /// <summary>
        /// Unique identifier
        /// </summary>
        public int Id { get; set; }

        public string Name { get; set; }

        public BuildingType BuildType { get; set; }


        public Building() { }

        public Building(int id, string name, BuildingType building, float x, float y)
        {
            Id = id;
            Name = name;
            X = x;
            Y = y;
            BuildType = building;
        }

        public override string ToString()
        {
            return $"{BuildType} at ({X},{Y})";
        }

        protected bool Equals(Building other)
        {
            return Id == other.Id;
        }

        public override bool Equals(object? obj)
        {
            if (ReferenceEquals(null, obj))
            {
                return false;
            }
            if (ReferenceEquals(this, obj))
            {
                return true;
            }
            return obj.GetType() == this.GetType() && Equals((Building)obj);
        }

        public override int GetHashCode()
        {
            return Id;
        }
    }
}
