import System.IO
    ( hClose,
      hIsEOF,
      openFile,
      hGetLine,
      hPutStrLn,
      hPrint,
      Handle,
      IOMode(WriteMode, ReadMode) )
import Data.List

-- “As a Hokie, I will conduct myself with honor and integrity at all times.
-- I will not lie, cheat, or steal, nor will I accept the actions of those who do.”

main = do 
        in_handle <- openFile "input.txt" ReadMode
        out_handle <- openFile "output.txt" WriteMode
        main_loop in_handle out_handle []
        hClose in_handle
        hClose out_handle

main_loop :: Handle -> Handle -> [String] -> IO ()
main_loop in_handle out_handle [] = 
        do in_eof <- hIsEOF in_handle
           if in_eof 
                then return ()
                else do line <- hGetLine in_handle
                        let line_words = words line
                        process line_words [] [] out_handle False
                        main_loop in_handle out_handle []

process :: [String] -> [Int] -> [String] -> Handle -> Bool -> IO ()
process [] stack output handle error = do 
        let str_stack = convert_stack stack
        let final_stack = convert_output str_stack

        let printed = convert_output output
        if error
                then hPutStrLn handle "(illegal,illegal)"
        else do
                hPrint handle (printed, final_stack)

-- pop off and display
process (".S":xs) stack output handle error = do
        let new_output = output ++ convert_stack stack
        process xs stack new_output handle error

-- pop off and display
process (".":xs) stack output handle error = do
        if length stack < 1
                then process xs stack output handle True
        else do
                let new_stack  = init stack
                let popped     = reverse stack !! 0
                let new_output = output ++ [show popped]
                process xs new_stack new_output handle error

-- DROP 
process ("DROP":xs) stack output handle error = do
        if length stack < 1
                then process xs stack output handle True
        else do
                let new_stack = init stack
                process xs new_stack output handle error

-- DUP
process ("DUP":xs) stack output handle error = do
        if length stack < 1
                then process xs stack output handle True
        else do
                let new_stack = stack ++ [reverse stack  !! 0]
                process xs new_stack output handle error

-- SWAP 
process ("SWAP":xs) stack output handle error = do
        if length stack < 2
                then process xs stack output handle True
        else do
                let new_stack = init (init stack) ++ [reverse stack !! 0] ++ [reverse stack !! 1]
                process xs new_stack output handle error

-- OVER
process ("OVER":xs) stack output handle error = do 
        if length stack < 2
                then process xs stack output handle True
        else do
                let new_stack = stack ++ [reverse stack  !! 1]
                process xs new_stack output handle error 

-- ROT
process ("ROT":xs) stack output handle error = do 
        if length stack < 3
                then process xs stack output handle True
        else do
                let rev   = reverse stack
                let new_stack = reverse (take 2 rev ++ drop 3 rev) ++ [rev !! 2]
                process xs new_stack output handle error 

-- addition
process ("+":xs) stack output handle error = do 
        if length stack < 2
                then process xs stack output handle True
        else do
                let res = reverse stack !! 1 + reverse stack !! 0
                let new_stack = init(init stack)  ++ [res]
                process xs new_stack output handle error

-- subtraction
process ("-":xs) stack output handle error = do 
        if length stack < 2
                then process xs stack output handle True
        else do
                let res = reverse stack !! 1 - reverse stack !! 0
                let new_stack = init(init stack)  ++ [res]
                process xs new_stack output handle error

-- multiplication
process ("*":xs) stack output handle error = do 
        if length stack < 2
                then process xs stack output handle True
        else do
                let res = reverse stack !! 1 * reverse stack !! 0
                let new_stack = init(init stack)  ++ [res]
                process xs new_stack output handle error

process ("/":xs) stack output handle error = do 
        if length stack < 2
                then process xs stack output handle True
        else do
                let res = reverse stack !! 1 `div` reverse stack !! 0
                let new_stack = init(init stack) ++ [res]
                process xs new_stack output handle error

-- add number to stack
process (x:xs) stack output handle error = do
        let new_stack = stack ++ [read x :: Int]
        process xs new_stack output handle error

convert_stack :: [Int] -> [String]
convert_stack = map show

convert_output :: [String] -> String
convert_output = intercalate " " 
