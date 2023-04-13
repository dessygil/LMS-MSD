import { getAccessToken, withApiAuthRequired } from '@auth0/nextjs-auth0';
import jwt from 'jsonwebtoken';

export default async function getProtectedData(req, res) {
  const accessToken = await getAccessToken(req, res);

  if (!accessToken) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  console.log(accessToken);
  try {
    const response = await fetch('http://127.0.0.1:8000/public', {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });
    const data = await response.json();
    return res.status(200).json({ data });

  } catch (error) {

    console.error(error);
    return res.status(500).json({ error: 'Internal Server Error' });
  }
}
