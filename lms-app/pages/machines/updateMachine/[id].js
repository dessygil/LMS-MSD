import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';

const UpdateMachine = () => {
  const [name, setName] = useState('');
  const [modelNumber, setModelNumber] = useState('');
  const [manufacturer, setManufacturer] = useState('');
  const [timeTakes, setTimeTakes] = useState('');
  const [notes, setNotes] = useState('');
  
  const router = useRouter();
  const { id } = router.query;

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`http://api.localhost:8000/main/machines/${id}`);
        const machine = response.data;
        setName(machine.name);
        setModelNumber(machine.model_number);
        setManufacturer(machine.manufacturer);
        setTimeTakes(machine.time_takes);
        setNotes(machine.notes);
      } catch (error) {
        console.error('Error fetching machine:', error);
      }
    };

    if (id) {
      fetchData();
    }
  }, [id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.put(`http://api.localhost:8000/main/machines/${id}/update/`, {
        name: name,
        model_number: modelNumber,
        manufacturer: manufacturer,
        time_takes: timeTakes,
        notes: notes,
      });
      router.push(`/machines/${id}`);  // Redirect to machine detail page after update
    } catch (error) {
      console.error('Error updating machine:', error);
    }
  };

  return (
    <div>
      <h1>Update Machine</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Name:
          <input type="text" value={name} onChange={e => setName(e.target.value)} />
        </label>
        <label>
          Model Number:
          <input type="text" value={modelNumber} onChange={e => setModelNumber(e.target.value)} />
        </label>
        <label>
          Manufacturer:
          <input type="text" value={manufacturer} onChange={e => setManufacturer(e.target.value)} />
        </label>
        <label>
          Time Takes:
          <input type="text" value={timeTakes} onChange={e => setTimeTakes(e.target.value)} />
        </label>
        <label>
          Notes:
          <input type="text" value={notes} onChange={e => setNotes(e.target.value)} />
        </label>
        <button type="submit">Update</button>
      </form>
    </div>
  );
};

export default UpdateMachine;
