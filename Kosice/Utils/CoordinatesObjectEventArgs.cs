using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Kosice.Model;

namespace Kosice.Utils
{
    public class ObjectOnCoordinatesEventArgs : EventArgs
    {
        public ObjectOnCoordinatesEventArgs(ObjectOnCoordinates objOnCoords)
        {
            ObjectWithCoordinates = objOnCoords;
        }
        public ObjectOnCoordinates ObjectWithCoordinates { get; set; }
    }
}
