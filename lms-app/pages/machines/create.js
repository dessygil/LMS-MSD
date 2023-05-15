import React, { useState } from 'react'

const Create = () => {
  const [name, setName] = useState('')
  const [modelNumber, setModelNumber] = useState('')
  const [manufacturer, setManufacturer] = useState('')
  const [duration, setDuration] = useState('')
  const [notes, setNotes] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()

    const response = await fetch(
      'http://api.localhost:8000/main/machines/create/',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: name,
          model_number: modelNumber,
          manufacturer: manufacturer,
          duration: duration,
          notes: notes,
        }),
      },
    )

    if (response.ok) {
      alert('Machine created successfully')
    } else {
      console.log('Error data:', responseData)
      alert('Error creating machine')
    }
  }

  return (
    <div className="container mx-auto">
      <h1 className="text-2xl mb-4">Create Machine</h1>
      <form onSubmit={handleSubmit}>
        <label for="name">Name:</label>
        <input
          type="text"
          id="name"
          name="name"
          placeholder="Enter your name"
          onChange={(e) => setName(e.target.value)}
        ></input>

        <label for="model">Model:</label>
        <input
          type="text"
          id="model"
          name="model"
          placeholder="Enter the model"
          onChange={(e) => setModelNumber(e.target.value)}
        ></input>

        <label for="Manufacturer">Manufacturer:</label>
        <input
          type="text"
          id="Manufacturer"
          name="Manufacturer"
          placeholder="Enter the manufacturer"
          onChange={(e) => setManufacturer(e.target.value)}
        ></input>

        <label for="Time">Time:</label>
        <input
          type="number"
          id="Time"
          name="Time"
          min="1"
          max="10000"
          step="1"
          onChange={(e) => setDuration(e.target.value)}
        ></input>

        <label for="notes">Notes:</label>
        <textarea
          id="notes"
          name="notes"
          rows="4"
          cols="40"
          onChange={(e) => setNotes(e.target.value)}
        ></textarea>

        <button
          type="submit"
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Create
        </button>
      </form>
    </div>
  )
}

export default Create
