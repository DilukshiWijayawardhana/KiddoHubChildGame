using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using MongoDB.Driver;
using MongoDB.Bson;
using UnityEngine.UI;
using System;
using UnityEngine.SceneManagement;

public class Login : MonoBehaviour
{
    //MongoClient client = new MongoClient("mongodb+srv://airstudiolk:k479q8fxdWt8fro7@cluster0.am0uxk6.mongodb.net/?retryWrites=true&w=majority");
    MongoClient client = new MongoClient("mongodb+srv://kamaldesilva919:LROBZuFIdDsZLVJj@childdaycare.zxlal0y.mongodb.net/?retryWrites=true&w=majority&appName=ChildDaycare");

    
    IMongoDatabase database;
    IMongoCollection<BsonDocument> collection;

    public InputField usernameInput;
    public InputField passwordInput;

    public static string loggedInUsername; // Static variable to store logged-in username

    void Start()
    {
        database = client.GetDatabase("test");
        collection = database.GetCollection<BsonDocument>("students");
    }

    public void LoginUser()
    {
        string username = usernameInput.text;
        string password = passwordInput.text;

        var filter = Builders<BsonDocument>.Filter.Eq("studentName", username);
        var user = collection.Find(filter).FirstOrDefault();

        if (user != null)
        {
            string storedPassword = user["telephone"].AsString;

            if (password == storedPassword)
            {
                Debug.Log("Login successful!");

                // Set the static variable to the logged-in username
                loggedInUsername = username;

                // Load Scene 1
                SceneManager.LoadScene(1);
            }
            else
            {
                Debug.Log("Invalid password. Please try again.");
            }
        }
        else
        {
            Debug.Log("User not found. Please check your username.");
        }
    }
}
