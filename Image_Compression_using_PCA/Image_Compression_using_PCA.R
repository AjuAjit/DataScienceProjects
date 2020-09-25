#===========================================================================================
# 1. An application which will compress images all the .jpg files in a folder using PCA and 
# store them in the destination folder.
# 2. A clarity parameter is given as input. We choose minimum number of principle components
# that can capture atleast ___ % of variance in the original image. 
# 3. Pixel corrections are made to handle white background.
# 4. User is asked if he wants to keep the original images or not.

PCA_Compression <- function(source_path,destination_path, clarity)
{
  
  files <- list.files(path=source_path, pattern="*jpg", full.names=TRUE, recursive=FALSE)
  
  for (x in files)  {
    
    image = readJPEG(x)
    if (dim(image)[1] < dim(image)[2])
    {
      max_pcs = dim(image)[1]-1
      
    } else {
      max_pcs = dim(image)[2]
    }
    
    pca_comps_count_options_list = c(5,10,ceiling(max_pcs/16),ceiling(max_pcs/8),ceiling(max_pcs/4),ceiling(max_pcs/2),ceiling(max_pcs))
    
    r = image[,,1]
    g = image[,,2]
    b = image[,,3]
    
    image.r.pca = prcomp(r, center = FALSE)
    image.g.pca = prcomp(g, center = FALSE)
    image.b.pca = prcomp(b, center = FALSE)
    
    rgb.pca = list(image.r.pca, image.g.pca, image.b.pca)
    
    for (ncomp in pca_comps_count_options_list)
    {
      
      R = image.r.pca$x[,1:ncomp] %*% t(image.r.pca$rotation[,1:ncomp])
      G = image.g.pca$x[,1:ncomp] %*% t(image.g.pca$rotation[,1:ncomp])
      B = image.b.pca$x[,1:ncomp] %*% t(image.b.pca$rotation[,1:ncomp])
      
      R = ifelse(R>1, 1, R)
      R = ifelse(R<0, 0, R)
      
      G = ifelse(G>1, 1, G)
      G = ifelse(G<0, 0, G)
      
      B = ifelse(B>1, 1, B)
      B = ifelse(B<0, 0, B)
      
      img = array(c(R,G,B), dim = c(dim(image)[1:2],3))
      
      cr = img[,,1]
      cg = img[,,2]
      cb = img[,,3]
      
      var_original_r = sum(apply(r,2,var))
      var_compressed_r = sum(apply(cr,2,var))
      var_in_r = (var_compressed_r/var_original_r) * 100
      
      var_original_g = sum(apply(g,2,var))
      var_compressed_g = sum(apply(cg,2,var))
      var_in_g = (var_compressed_g/var_original_g) * 100
      
      
      var_original_b = sum(apply(b,2,var))
      var_compressed_b = sum(apply(cb,2, var))
      var_in_b = (var_compressed_b/var_original_b) * 100
      
      if((var_in_r > clarity) & (var_in_g > clarity) & (var_in_b > clarity))
      {
        print(paste("For given clarity, minimum number of PCs needed are ",ncomp))
        print(paste(var_in_r,var_in_g,var_in_b))
        setwd("D:/Praxis/ML/Images/Compressed_images")
        writeJPEG(img, paste(substr(x, nchar(x)-10,nchar(x)-4),".jpg",sep=""))        
        break
      }
      
      setwd(destination_path)
      writeJPEG(img, paste(substr(x, nchar(x)-10,nchar(x)-4),".jpg",sep=""))
      
    }
    
  }
  my.option <- readline(prompt="Do you want to delete your original files? Y/N ")
  if(my.option == "Y")
  {
    for(y in files)
    {
      file.remove(y)
    }
  }
  
}

PCA_Compression("D:/Praxis/ML/Images","D:/Praxis/ML/Images/Compressed_images",25)

