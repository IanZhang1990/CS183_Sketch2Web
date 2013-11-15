using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using SetSimilarity;
using System.IO;

namespace MinHashProgram
{
    class Program
    {
        static void Main(string[] args)
        {
            int[] array1 = {1,2,3,4,5,6,7,8,9, 0};
            int[] array2 = { 1, 2, 3, 4, 5, 6, 7, 8, 0, 0};
            int[] array3 = { 0 };
            HashSet<int> set1 = new HashSet<int>(array1);
            HashSet<int> set2 = new HashSet<int>(array2);
            HashSet<int> set3 = new HashSet<int>(array3);

            MinHash minHash = new MinHash(10);
            double similarity = minHash.Similarity<int>(set1, set3);
            System.Console.WriteLine(similarity);

            myFileReader filereader = new myFileReader("menu-edge.txt");
            myFileReader filereader2 = new myFileReader("web-menu-edge.txt");
            List<double> list1 = filereader.GetArray();
            List<double> list2 = filereader2.GetArray();
            HashSet<double> featureSet = new HashSet<double>(list1);
            HashSet<double> featureSet2 = new HashSet<double>(list2);

            MinHash minHash2 = new MinHash(list1.Count + list2.Count);
            double similarity2 = minHash2.Similarity(featureSet, featureSet2);
            System.Console.WriteLine(similarity2);
        }
    }
}
