 using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;
using MongoDB.Driver;
using MongoDB.Bson;
using System;

public class connect : MonoBehaviour
{
    public static string suggetion;
    public int level1 = 1;
    public int level2 = 1;
    public int level3 = 1;

    public string username = "defult";
   
    public int pstatus = 1;
    // public int suggetion = 1;

    public static int Remotion;
  //  public GameObject TextH;


    public Text TextFild;
    public Text ScorTextFild1;
    public Text ScorTextFild2;
    public Text ScorTextFild3;

    public string url;



    //Mongo Db 
    MongoClient client = new MongoClient("mongodb+srv://kamaldesilva919:LROBZuFIdDsZLVJj@childdaycare.zxlal0y.mongodb.net/?retryWrites=true&w=majority&appName=ChildDaycare");
    IMongoDatabase database;
    IMongoCollection<BsonDocument> collection;


    // Start is called before the first frame update
    void Start()
    {

        database = client.GetDatabase("test");
        collection = database.GetCollection<BsonDocument>("highscorecollections");
        // seturl();

        // WWW www = new WWW(url);
        // StartCoroutine(WaitForRequest(www));
        sendserverRequest();
        
    }

    float elapsed = 0f;
    int num = 1;

   void Update()
    {

        // seturl();
        // //Time delay with 5sec
        // elapsed += Time.deltaTime;
        // if (elapsed >= 5f)
        // {
        //     elapsed = elapsed % 5f;
           
        //     num = num + 1;
        
        //     WWW www = new WWW(url);
        //     StartCoroutine(WaitForRequest(www));
        //     // settext();
        // }

    }
    void seturl()
    {

        level1 = QuizGame.scoresetlevel1;
        level2 = QuizGameLevel2.scoresetlevel2;
        level3 = QuizGameLevel3.scoresetlevel3;
        username = Login.loggedInUsername;

        

        url = "http://127.0.0.1:5000/gamepredict?v1=" + level1+"&v2="+level2+"&v3="+level3;
    }

   
    // Send Request
    
    
    public void settext()
    {
        TextFild.text = suggetion;
        ScorTextFild1.text = level1.ToString();
        ScorTextFild2.text = level2.ToString();
        ScorTextFild3.text = level3.ToString();
        InsertDefaultData();
    //    TextH.GetComponent<Text>().text = "Emotion:" + emotion;
    }

    public void sendserverRequest()
    {
        // quize = int.Parse(Rediobutton.Qname);
        // status = Rediobutton.QuizstatusNUM;
        StartCoroutine(sendRequest());
    }
    
    IEnumerator sendRequest()  // user Regitation
   {
     seturl();

        WWW www = new WWW(url);
        StartCoroutine(WaitForRequest(www));

           yield return www;
        if(www.error == null)
        {
            // Debug.Log("resultE:" + www.text);
            suggetion = www.text;
            print(suggetion);
            settext();
        }
        else
        {
            Debug.Log("www error:" + www.error);
        }
   }


    IEnumerator WaitForRequest(WWW www)
    {
        yield return www;
        if(www.error == null)
        {
            // Debug.Log("resultE:" + www.text);
            suggetion = www.text;
            print(suggetion);
             Debug.Log("1st step");
            // settext();

        }
        else
        {
            Debug.Log("www error:" + www.error);
        }
    }


//----------------------------Mongo DB--------------------------------------------------

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
        InsertDataToDB(username, level1, level2, level3, suggetion, DateTime.Now.ToString());
       // InsertDataToDB("Jane Smith", 78, 80, 85, "Intermediate", DateTime.Now.ToString());
       // InsertDataToDB("Alice Johnson", 95, 92, 88, "Advanced", DateTime.Now.ToString());

        Debug.Log("User data inserted into the database.");
    }

}
