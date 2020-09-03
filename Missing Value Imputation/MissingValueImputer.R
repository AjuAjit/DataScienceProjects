#===========================================================================================
# CREATING A FUNCTION OF OUR OWN
#===========================================================================================

# We spend a lot of time dealing with missing values in any dataset.Wouldn't it save 
# a lot of time if we had a function which deals with the problem of missing values?

# Keeping this in mind, I have developed a function to handle missing values.

# This function has been written in a generalised way to be able to handle any dataset.
# But it's important to remember that, each dataset is unique and there are 
# many associations present between variables, and these associations will not be taken into
# consideration while imputing values using our function.

# Let's look at the algorithm behind the function now.

# 1.Iterate for i = 1 to number of variables
  # 2. Checks if more than p% observations of ith variable are NAs.
  #   - If yes, drop ith variable.
  #   - Otherwise, go to step 2.
  # 3. Check if the variable is categorical.
  #   - If yes, use mode of the variable to impute missing value.
  #   - Otherwise, go to step 3.
  # 4. Find the mean and median of the variable.
  # 5. If the mean is very far from the median on either side, use median imputation.
  # 6. If mean is reasonably close to the median, use mean imputation.
# End Loop
# 7. Check if there are no more missing values.
# 8. Return


str(fram)

install.packages("moments")
library(moments)

fram = read.csv("D:\\Praxis\\ML\\data\\framingham.csv")
View(fram)
str(fram)



missing_value_imputer <- function(data)
{
  
  for(target in 1:ncol(data))
  {
    tname = names(data)[target]
    dropped_cols = c()
    i = 0
    if(sum(is.na(data[,target]))/nrow(data) > 0)
    {
      if(sum(is.na(data[,target]))/nrow(data) * 100 > 90)
      {
        dropped_cols[i] = names(data)[target]
      }
      else
      {
        if ((length(unique(data[,target])) < 10) | (is.character(data[,target])) | (is.factor(data[,target])))
        {
          print(paste(names(data)[target],"- categorical mode"))
          sort(table(data[,target]))
          if(is.numeric(data[,target]))
          {
            print(as.numeric(names(table(data[,target]))[table(data[,target])==max(table(data[,target]))]))
            data[,target][is.na(data[,target])] = (as.numeric(names(table(data[,target]))[table(data[,target])==max(table(data[,target]))]))
          }
          else
          {
            print(names(table(data[,target]))[table(data[,target])==max(table(data[,target]))])
            data[,target][is.na(data[,target])] = (names(table(data[,target]))[table(data[,target])==max(table(data[,target]))])
          }
        }
        else
        {
          if((skewness(data[,target],na.rm = TRUE))>1 | (skewness(data[,target],na.rm = TRUE)< (-1)))
          {
            print(paste(names(data)[target],"- Numerical- median"))
            print(median(data[,target],na.rm = TRUE))
            data[,target][is.na(data[,target])] = (median(data[,target],na.rm = TRUE))
          }
          else
          {
            print(paste(names(data)[target],"- Numerical- mean"))
            print(mean(data[,target],na.rm = TRUE))
            data[,target][is.na(data[,target])] = (mean(data[,target],na.rm = TRUE))
          }
        }
      }
    }
  }
  return(data)
}

fram1 = missing_value_imputer(fram)

sum(is.na(fram1))


