const express = require('express')
const fs = require('fs')
const cors = require("cors")
const app = express()
const port = 8080
app.use(cors())

app.get('/', (req, res) => {
  try {
    const data = fs.readFileSync('./capacity_data.txt', 'utf8')
    res.send(data)
  } catch (err) {
    console.error(err)
    res.send('oops')
  }
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})