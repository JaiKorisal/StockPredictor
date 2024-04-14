'use client'

import { AiOutlineSearch } from 'react-icons/ai'
import Link from 'next/link'
import React, { useState } from 'react'

const page = () => {
  function addClassAndClub() {
    const [val, setVal] = useState([])
  }
  return (
    <main className='flex min-h-screen flex-col items-center justify-between p-24'>
      <form className='flex flex-col items-center'>
        <div className='z-10 w-full max-w-5xl items-center justify-between font-mono text-sm lg:flex'>
          <Link className='font-mono font-bold' href='/search'>
            Settings
          </Link>
        </div>
        <div className={`mb-3 text-2xl font-bold text-center`}>
          <h1 className={`mb-3 text-2xl font-semibold`}>
            What is your question?
          </h1>
        </div>
        <div className='w-[500px] relative'>
          <input
            type='search'
            placeholder='Type Here'
            className='w-full p-4 rounded-full bg-slate-800 text-white'
          />
          <button className='absolute right-1 top-1/2 -translate-y-1/2 p-4 bg-slate-400 rounded-full'>
            <AiOutlineSearch />
          </button>
        </div>
        <div className={`mb-3 text-2xl font-bold text-center mt-10`}>
          <h1>Examples:</h1>
          <div className={`mb-3 text-2xl font-semibold text-center mt-3`}>
            <h2>What club events are going on today?</h2>
            <h2>Who is the dean of the Engineering Department?</h2>
            <h2>How do I start my own club?</h2>
          </div>
        </div>
        <div className='mb-32 grid text-center lg:mb-0 lg:grid-cols-3 lg:text-left'>
          <a
            className='group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30'
            target='_blank'
            rel='noopener noreferrer'
          >
            <h2 className={`mb-3 text-2xl font-semibold`}>
              Search History<span>-&gt;</span>
            </h2>
            <p className={`m-0 max-w-[30ch] text-sm opacity-50`}>
              View your past questions here.
            </p>
          </a>
          <a
            href='/Dashboard'
            className='group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30'
            target='_blank'
            rel='noopener noreferrer'
          >
            <h2 className={`mb-3 text-2xl font-semibold`}>
              Dashboard{' '}
              <span className='inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none'>
                -&gt;
              </span>
            </h2>
            <p className={`m-0 max-w-[30ch] text-sm opacity-50`}>
              View your classes and clubs here.
            </p>
          </a>
          <a
            className='group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30'
            target='_blank'
            rel='noopener noreferrer'
          >
            <h2 className={`mb-3 text-2xl font-semibold`}>
              Calendar{' '}
              <span className='inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none'>
                -&gt;
              </span>
            </h2>
            <p className={`m-0 max-w-[30ch] text-sm opacity-50`}>
              View what's coming up here.
            </p>
          </a>
        </div>
      </form>
    </main>
  )
}

export default page