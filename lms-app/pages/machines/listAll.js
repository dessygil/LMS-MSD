// MachineList.js
import React, { useState, useEffect } from 'react';

const MachineList = () => {
  const [machines, setMachines] = useState([]);


    //TODO 
  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch('http://api.localhost:8000/main/machines/');
      const data = await response.json();
      setMachines(data);
    };

    fetchData();
  }, []);

  return (
    <div>
      <h1>Machine List</h1>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Model Number</th>
            <th>Manufacturer</th>
            <th>Time Takes</th>
            <th>Notes</th>
          </tr>
        </thead>
        <tbody>
          {machines.map((machine) => (
            <tr key={machine.id}>
              <td>{machine.id}</td>
              <td>{machine.name}</td>
              <td>{machine.model_number}</td>
              <td>{machine.manufacturer}</td>
              <td>{machine.time_takes}</td>
              <td>{machine.notes}</td>
                
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default MachineList;