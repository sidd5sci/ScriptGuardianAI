@Grab(group='org.mongodb', module='mongo-java-driver', version='3.12.10')

import com.mongodb.MongoClientURI
import com.mongodb.MongoClient
import com.mongodb.client.MongoDatabase
import org.bson.Document

def mongoUrl = "mongodb://admin:supersecret@localhost:27017/?authSource=admin"

println "Connecting using: $mongoUrl"

MongoClientURI uri = new MongoClientURI(mongoUrl)
MongoClient mongoClient = new MongoClient(uri)
MongoDatabase database = mongoClient.getDatabase("test")

def collection = database.getCollection("users")
println "Fetched users collection successfully."

def filter = new Document("active", true)
println "Prepared filter for active users."

println "Connected to MongoDB."
mongoClient.close()