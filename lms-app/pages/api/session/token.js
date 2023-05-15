import { withApiAuthRequired } from '@auth0/nextjs-auth0'
import axios from 'axios'

async function handler(req, res) {
  try {
    const accessTokenRequest = await axios.post(
      `${process.env.AUTH0_ISSUER_BASE_URL}/oauth/token`,
      {
        client_id: process.env.AUTH0_CLIENT_ID,
        client_secret: process.env.AUTH0_CLIENT_SECRET,
        audience: process.env.AUTH0_AUDIENCE_02,
        grant_type: 'client_credentials',
      },
    )

    const accessTokenData = accessTokenRequest.data

    const privateApiEndpointResponse = await axios.get(
      'http://api.localhost:8000/api/private',
      {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${accessTokenData.access_token}`,
        },
      },
    )

    const privateApiEndpointData = privateApiEndpointResponse.data

    res.status(privateApiEndpointResponse.status).json(privateApiEndpointData)
  } catch (error) {
    console.log('There was an error with status code: ', error.response.status)
  }
}

export default withApiAuthRequired(handler)
