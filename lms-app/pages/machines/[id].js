import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';

//TODO use only axios or fetch, I will be using axios for now

const Machine = () => {
  const [machine, setMachine] = useState(null);
  const router = useRouter();
  const { id } = router.query;

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(`http://api.localhost:8000/main/machines/${id}`);
                setMachine(response.data);
            } catch (error) {
                console.error('Error fetching machine:', error);
            }
        };
        if (id) {
            fetchData();
        }
    }, [id]);

    const handleDelete = async () => {
        try {
            await axios.delete(`http://api.localhost:8000/main/machines/${id}`);
            router.push('/machines/listAll');  // Redirect to home page after delete
        } catch (error) {
            console.error('Error deleting machine:', error);
        }
    };

    const handleUpdate = async () => {
        try {
            router.push(`/machines/updateMachine/${id}`);
        } catch (error) {
            console.error('Machine not found:', error);
        }
    };

    if (!machine) {
        return <div>Loading...</div>;
    }

    return (
        <>
            <div>
                <h1>{machine.name}</h1>
                <p>ID: {machine.id}</p>
                <p>Model Number: {machine.model_number}</p>
                <p>Manufacturer: {machine.manufacturer}</p>
                <p>Time Takes: {machine.time_takes}</p>
                <p>Notes: {machine.notes}</p>
            </div>
            <button onClick={handleUpdate}>Update</button>
            <button onClick={handleDelete}>Delete</button>
        </>
    );
};

export default Machine;
