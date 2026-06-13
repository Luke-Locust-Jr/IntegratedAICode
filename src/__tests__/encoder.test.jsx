import React from 'react'
import '../setupTests'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import InvertedMathEncoder from '../components/InvertedMathEncoder'
import { beforeEach, test, expect } from 'vitest'

beforeEach(() => {
  localStorage.clear()
})

test('encoder round-trip and logs metadata', async () => {
  render(<InvertedMathEncoder />)
  const input = screen.getByPlaceholderText(/enter a sentence/i)
  await userEvent.type(input, 'hi')
  const btn = screen.getByRole('button', { name: /encode/i })
  await userEvent.click(btn)

  // Expect output to appear
  const output = await screen.findByText('hi', { selector: 'code' })
  expect(output).toBeInTheDocument()

  // Meta log should contain an entry
  const raw = localStorage.getItem('positron_imaging_meta_log')
  expect(raw).not.toBeNull()
  const arr = JSON.parse(raw)
  expect(Array.isArray(arr)).toBe(true)
  expect(arr.length).toBeGreaterThanOrEqual(1)
  expect(arr[0].source).toBe('InvertedMathEncoder')
})
