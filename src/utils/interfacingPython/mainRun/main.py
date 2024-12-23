import PoissonPointAllocation as qbn

def main():
    xRecMin = 0
    xRecMax = 50
    yRecMin = 0
    yRecMax = 50

    xp=[xRecMin, xRecMax, xRecMax, xRecMin, xRecMin]
    yp=[yRecMin,yRecMin, yRecMax, yRecMax, yRecMin]
    allocator = qbn.PoissonProcess(xp, yp)


if __name__ == "__main__":
    main()