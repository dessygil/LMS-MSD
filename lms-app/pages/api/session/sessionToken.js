import { getAccessToken, withApiAuthRequired } from '@auth0/nextjs-auth0';

export default withApiAuthRequired(async function apiEndpoint(req, res) {
  try {
    const { accessToken } = await getAccessToken(req, res);
    console.log('Access Token:', accessToken);
    res.status(200).json({ success: true });
  } catch (error) {
    console.error(error);
    res.status(error.status || 500).end(error.message);
  }
});
