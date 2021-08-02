  PROGRAM hello_world
  USE OMP_LIB

  !$OMP PARALLEL
  PRINT *, "Hello from thread: ", OMP_GET_THREAD_NUM()
  !$OMP END PARALLEL

  END PROGRAM hello_world 
