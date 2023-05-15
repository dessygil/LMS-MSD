import { getAccessToken, withApiAuthRequired } from '@auth0/nextjs-auth0'

export default withApiAuthRequired(async function ProtectedRoute(req, res) {
  const accessData = await getAccessToken(req, res)

  if (!accessData) {
    return res.status(401).json({ error: 'Unauthorized' })
  }

  try {
    const response = await fetch('http://api.localhost:8000/api/private', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${accessData.accessToken}`,
      },
    })
    const data = await response.json()
    return res.status(200).json({ data })
  } catch (error) {
    return res.status(500).json({ error: 'Internal Server Error' + error })
  }
})
