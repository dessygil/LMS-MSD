import { getAccessToken, withApiAuthRequired} from '@auth0/nextjs-auth0';

export default withApiAuthRequired(async function products(req, res) {
  const accessToken = await getAccessToken(req, res);
  if (!accessToken) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  try {
    const response = await fetch('http://api:8000/api/private', {
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
});