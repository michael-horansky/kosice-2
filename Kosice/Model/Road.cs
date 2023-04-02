using System;
using System.Collections.Generic;
using Kosice.Model;

namespace Kosice.Model;

/// <summary>
/// Represents shark attack
/// </summary>
public class Road
{
    /// <summary>
    /// Unique identifier
    /// </summary>
    public int Begin { get; set; }

    public int End { get; set; }
    public Road()
    {

    }

    public Road(int fromId, int toId)
    {
        Begin = fromId;
        End = toId;
    }

    public override string ToString()
    {
        return $"Road between {Begin} and {End}";
    }

    protected bool Equals(Road other)
    {
        return Begin == other.Begin && End == other.End;
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
        return obj.GetType() == this.GetType() && Equals((Road)obj);
    }

    public override int GetHashCode()
    {
        return Begin.GetHashCode() ^ End.GetHashCode();
    }

    public float PhysicalLength(Dictionary<int, Intersection> intersections)
    {
        return intersections[this.FromId].DistanceToOtherLocation(
            intersections[this.ToId]
        );

    }
}