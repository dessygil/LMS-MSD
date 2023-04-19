import { getAccessToken, withApiAuthRequired } from '@auth0/nextjs-auth0';


export default withApiAuthRequired(async function ProtectedRoute(req, res) {
    const accessData = await getAccessToken(req, res);
    if (!accessData) {
        return res.status(401).json({ error: 'Unauthorized' });
    }
    try {
        return res.status(200).json({ accessToken: accessData.accessToken });
    } catch (error) {
        return res.status(500).json({ error: 'Internal Server Error' + error });
    }
});
