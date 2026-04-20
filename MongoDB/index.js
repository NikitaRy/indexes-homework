const { MongoClient } = require("mongodb");

const uri = "mongodb+srv://kiselevsereja_db_user:EzoQXaG8JEj5vs5Z@test.elrafha.mongodb.net/?appName=test";

const client = new MongoClient(uri);

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

function getIndexName(plan) {
  if (plan.stage === "IXSCAN") return plan.indexName;
  if (plan.inputStage) return getIndexName(plan.inputStage);
  if (plan.shards) return getIndexName(plan.shards[0].winningPlan);
  return "No Index Used";
}

async function run() {
  try {
    await client.connect();
    const db = client.db("sample_mflix");
    const movies = db.collection("movies");

    try { await movies.dropIndexes(); } catch (e) {}

    // Задание 1: Поиск фильмов с определенным актерским дуэтом
    console.log("\n--- Задание 1: Поиск фильмов с определенным актерским дуэтом ---");
    const task1 = await movies.find({ 
      cast: { $all: ["Tom Hanks", "Tim Allen"] } 
    }).project({ title: 1, year: 1, cast: 1, _id: 0 }).toArray();
    console.log(task1);

    // Задание 2: Анализ по десятилетиям
    console.log("\n--- Задание 2: Анализ по десятилетиям ---");
    const task2 = await movies.aggregate([
      { $match: { year: { $gte: 1900, $lte: 1999 }, runtime: { $type: "number" } } },
      { $project: { runtime: 1, decade: { $subtract: ["$year", { $mod: ["$year", 10] }] } } },
      { $group: { _id: "$decade", avgRuntime: { $avg: "$runtime" } } },
      { $sort: { _id: 1 } }
    ]).toArray();
    console.table(task2);

    // Задание 3: Поиск фильмов с наибольшим количеством комментариев
    console.log("\n--- Задание 3: Поиск фильмов с наибольшим количеством комментариев ---");
    const task3 = await movies.find({})
      .sort({ num_mflix_comments: -1 }).limit(10)
      .project({ title: 1, num_mflix_comments: 1, _id: 0 }).toArray();
    console.table(task3);

    // Задание 4: Гибкая схема
    console.log("\n--- Задание 4: Гибкая схема ---");
    const res = await movies.insertOne({ title: "Test Movie", type: "custom_type", custom_field: true });
    console.log(`Документ добавлен: ${res.insertedId}`);
    await movies.deleteOne({ _id: res.insertedId });

    // Задание 5: Анализ эффективности покрывающего индекса
    console.log("\n--- Задание 5: Анализ эффективности покрывающего индекса ---");
    await movies.createIndex({ year: 1, "imdb.rating": -1, title: 1 }, { name: "CoveredIdx" });
    await sleep(1000); 

    const query5 = movies.find({ year: 2010, "imdb.rating": { $type: "number" } })
      .sort({ "imdb.rating": -1 }).limit(5)
      .project({ year: 1, "imdb.rating": 1, title: 1, _id: 0 });

    const explain5 = await query5.explain("executionStats");
    const docs5 = await query5.toArray();
    console.table(docs5);
    console.log(`Docs Examined: ${explain5.executionStats.totalDocsExamined}`);

    // Задание 6: Индексация массивов
    console.log("\n--- Задание 6: Индексация массивов ---");
    await movies.createIndex({ genres: 1 }, { name: "GenresIdx" });
    await sleep(1000);

    const query6 = movies.find({ genres: { $all: ["Action", "Sci-Fi"] } })
      .project({ title: 1, genres: 1, _id: 0 }).limit(5);

    const explain6 = await query6.explain("executionStats");
    const docs6 = await query6.toArray();
    console.table(docs6);
    
    const plan6 = explain6.queryPlanner ? explain6.queryPlanner.winningPlan : explain6.executionStats.executionStages;
    console.log(`Index Used: ${getIndexName(plan6)}`);

  } catch (e) {
    console.error(e);
  } finally {
    await client.close();
  }
}

run();