import { render, screen } from '@testing-library/react'
import Header from '../pages/components/Header'
import '@testing-library/jest-dom'

describe('Header', () => {
  it('renders correctly', () => {
    render(<Header />)
    expect(screen.getByTestId('header')).toBeInTheDocument()
  })
})
