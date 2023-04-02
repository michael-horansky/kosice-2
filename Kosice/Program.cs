using System.Collections.Generic;
using Kosice.DataLoading.DataContext;
using Kosice.DataLoading.Factory;
using Kosice.Model;
using Kosice.Utils;
using Kosice.Model.Enums;
using System;
using System.Collections;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Kosice;

class program
{
    static void Main()
    {
        RoadManager roadManager = new();
        //foreach (var road in roadManager.GetRoads())
        //{
        //    Console.WriteLine(road);
        //}
        Console.WriteLine(roadManager.GetRoads().Count);
        roadManager.AddRoad(4846566, 46);
        Console.WriteLine(roadManager.GetRoads().Count);
        roadManager.RemoveIntersection(4846566);
        Console.WriteLine(roadManager.GetRoads().Count);
        Console.ReadLine();
    }

    
}