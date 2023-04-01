using System;
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
    public int FromId { get; set; }

    public int ToId { get; set; }
    public Road()
    {

    }

    public Road(int fromId, int toId)
    {
        FromId = fromId;
        ToId = toId;
    }

    public override string ToString()
    {
        return $"Road between {FromId} and {ToId}";
    }

    protected bool Equals(Road other)
    {
        return FromId == other.FromId && ToId == other.ToId;
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
        return FromId.GetHashCode()^ToId.GetHashCode();
    }
}
