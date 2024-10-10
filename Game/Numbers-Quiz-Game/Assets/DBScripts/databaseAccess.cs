using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using MongoDB.Driver;
using MongoDB.Bson;
using UnityEngine.UI;
using System;

public class databaseAccess : MonoBehaviour
{
    MongoClient client = new MongoClient("mongodb+srv://airstudiolk:k479q8fxdWt8fro7@cluster0.am0uxk6.mongodb.net/?retryWrites=true&w=majority");
    IMongoDatabase database;
    IMongoCollection<BsonDocument> collection;

    // Start is called before the first frame update
    void Start()
    {
        database = client.GetDatabase("test");
        collection = database.GetCollection<BsonDocument>("HighScoreCollection");

        // Insert default data when the game starts
        InsertDefaultData();
    }

    // Update is called once per frame
    void Update()
    {
        // Update the date text
        // dateText.text = DateTime.Now.ToString();
    }

    public void InsertDataToDB(string studentName, int q1Marks, int q2Marks, int q3Marks, string knowledgeLevel, string date)
    {
        // Create a new document to insert into the collection
        var document = new BsonDocument
        {
            { "StudentName", studentName },
            { "Q1Marks", q1Marks },
            { "Q2Marks", q2Marks },
            { "Q3Marks", q3Marks },
            { "KnowledgeLevel", knowledgeLevel },
            { "Date", date }
        };

        // Insert the document into the collection
        collection.InsertOne(document);
        
        // Log to console for debugging
        Debug.Log("Data inserted into the database.");
    }

    private void InsertDefaultData()
    {
        // Insert default data here
        InsertDataToDB("John Doe", 85, 90, 95, "Advanced", DateTime.Now.ToString());
        InsertDataToDB("Jane Smith", 78, 80, 85, "Intermediate", DateTime.Now.ToString());
        InsertDataToDB("Alice Johnson", 95, 92, 88, "Advanced", DateTime.Now.ToString());

        Debug.Log("Default data inserted into the database.");
    }
}
