function sendTask() {
  let codeElement = document.getElementById("codeBox")
  let code = codeElement.value
  let python = document.getElementById("python").checked
  let cmd = document.getElementById("cmd").checked
  let repeating = document.getElementById("repeat").checked
  var type = ""
  if (python == true) {
    type = "python"
  }
  if (cmd == true) {
    type = "CMD"
  }
  let url = "/broadcast"
  let data = {
    type: type,
    code: code,
    repeating: repeating,
  }
  fetch(url, {
    method: 'POST', // Specify the request type
    headers: {
      'Content-Type': 'application/json',  // Specify the content type
    },
    body: JSON.stringify(data),  // Convert the data to JSON
  })
    .then(response => response.json())  // Parse the JSON response from the server
    .then(result => {
      console.log('Success:', result);  // Handle the success response
      codeElement.value = ""
      setTimeout(() => {
        makeElement(code)
      }, 2000)

    })
    .catch(error => {
      console.error('Error:', error);  // Handle errors
    });
}


function makeElement(code) {
  let url = "/collectOutput"
  fetch(url)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json(); // Parse the response as JSON
    })
    .then(data => {
      let codeWindow = document.getElementById("codeWindow")
      let oldElements = codeWindow.innerHTML
      let count = 0
      list = data.output 
      for (let i of list) {
        if (i[0] == "compilation succesfull") {
          count += 1
        }
      }

      let element3 = ""
      list = code.split("\n")
      for (let i of list) {
        element3 = element3 + `<div class="line">${i}</div>`
      }

      result = `Succesfully compiled in ${count} devices`

      let element = `<div class="codeElement">
            <div class="code">${element3}
            </div>
            <div class="output">
                ${result}
            </div>`

      codeWindow.innerHTML = oldElements+element
    })
}