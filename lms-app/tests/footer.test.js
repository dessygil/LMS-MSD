import { render, screen } from '@testing-library/react'
import Footer from '../pages/components/Footer'
import '@testing-library/jest-dom'

describe('Footer', () => {
  it('renders correctly', () => {
    render(<Footer />)
    expect(screen.getByTestId('footer')).toBeInTheDocument()
  })
})
